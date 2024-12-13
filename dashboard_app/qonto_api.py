import uuid

from django.conf import settings
from django.contrib.sites import requests
import requests
import pathlib, os, json
from django.template.defaultfilters import slugify

from tiqo_parser.models import Configuration, Label, Iban, Transaction, Category, QontoContact, Attachment
from tiqo_parser.serializers import LabelsSerializer


class QontoApi():
    def __init__(self):
        config = Configuration.get_solo()
        self.login = config.qonto_login
        self.api_key = config.qonto_apikey

        if not any([self.login, self.api_key]):
            raise Exception("No Qonto credentials. Set its in the admin panel.")

    def _get_request_api(self, url, params=None):
        url = f"https://thirdparty.qonto.com/v2/{url}"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"{self.login}:{self.api_key}"
        }

        response = requests.request("GET", url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()

        print(response.text)
        raise Exception(response.text)

    def get_all_ibans(self):
        info_orga = self._get_request_api("organization")
        if info_orga.get('organization'):
            if info_orga.get('organization').get('bank_accounts'):
                bank_accounts = info_orga.get('organization').get('bank_accounts')
                for acc in bank_accounts:
                    Iban.objects.get_or_create(
                        iban=acc.get('iban'),
                        name=acc.get('name'),
                    )

        return Iban.objects.all()

    def get_all_contacts(self):
        memberships_response_dict = self._get_request_api("memberships")
        members = memberships_response_dict.get('memberships')
        for member in members:
            QontoContact.objects.get_or_create(
                uuid=member.get('id'),
                last_name=member.get('last_name'),
                first_name=member.get('first_name'),
                type="M",
            )

        beneficiaries_response_dict = self._get_request_api("beneficiaries")
        for beneficiary in beneficiaries_response_dict.get('beneficiaries'):
            QontoContact.objects.get_or_create(
                uuid=beneficiary.get('id'),
                last_name=beneficiary.get('name'),
                type="B",
            )
        return QontoContact.objects.all()

    def get_all_external_transfers(self):
        all_external_transfers = []
        current_page = 1
        while current_page is not None:
            response_dict = self._get_request_api("external_transfers", params={
                'page': current_page
            })
            all_external_transfers += response_dict.get('external_transfers')
            current_page = response_dict.get('meta').get('next_page')
            print(f"get_external_transfers next page : {current_page}")

        for external_transfer in all_external_transfers:
            if external_transfer.get('transaction_id'):
                tr = Transaction.objects.filter(uuid=external_transfer.get('transaction_id'))
                contact = QontoContact.objects.filter(uuid=external_transfer.get('beneficiary_id'))
                if contact.exists() and tr.exists():
                    transaction = tr.first()
                    transaction.uuid_external_transfer = external_transfer.get('id')
                    transaction.reference = external_transfer.get('reference')
                    transaction.beneficiary = contact.first()
                    transaction.save()

                    print(f"ExternalTransfer {transaction.reference}")

        return all_external_transfers

    def fetch_all_transaction(self):
        # Mise à jour des IBAN
        ibans = self.get_all_ibans()

        transactions = {}
        # Qonto demande l'iban du compte pour récupérer les transactions
        for iban in ibans:
            transactions[iban] = []
            current_page = 1
            while current_page is not None:
                response_dict = self._get_request_api("transactions", params={
                    "iban": iban.iban,
                    "page": current_page,
                })
                if response_dict:
                    transactions[iban] += response_dict.get('transactions')
                    current_page = response_dict.get('meta').get('next_page')
                    print(f"fetch_all_transaction next page : {current_page}")

        return transactions

    def download_or_update_attachment(self, uuid_attachment: str, db_transaction: Transaction, download_file=False):
        # On va chercher l'attachment dans la base de données
        # Peut-être qu'il existe déja
        response_dict = self._get_request_api(f"attachments/{uuid_attachment}")
        attachment = response_dict.get('attachment')
        url = attachment.get('url')
        db_attachement = Attachment.objects.filter(uuid=uuid_attachment)
        if db_attachement.exists():
            db_attachement.update(
                url_qonto=url
            )
            print(f"EXIST attachment uuid : {db_attachement.first().name}")
            return db_attachement.first()

        else:

            if attachment:
                file_content_type = attachment.get('file_content_type')
                file_ext = file_content_type.partition('/')[-1]
                file_name = f"{attachment['id']}.{file_ext}"
                full_path_file = None

                if download_file:
                    fetch_file_url = requests.get(url)
                    print(f"fetch_file_url.status_code : {fetch_file_url.status_code}")

                    if fetch_file_url.status_code == 200:
                        path_media = f"{settings.MEDIA_ROOT}/" \
                                     f"{slugify(db_transaction.iban.name)}/" \
                                     f"{slugify(db_transaction.emitted_at.date())}/" \
                                     f"{db_transaction.side}/" \
                                     f"{db_transaction.uuid}/"

                        path = pathlib.Path(path_media)
                        pathlib.Path(f"{path_media}").mkdir(parents=True, exist_ok=True)

                        full_path_file = f"{path}/{file_name}"
                        with open(full_path_file, 'wb') as f:
                            f.write(fetch_file_url.content)
                        print(f"NEW attachement downloaded : {full_path_file}")

                db_attachement, created = Attachment.objects.get_or_create(
                    uuid=attachment['id'],
                    # filepath=full_path_file,
                    url_qonto=url,
                    name=attachment['file_name'],
                )
                print(f"NEW attachement created : {db_attachement.name}")

                db_attachement.transactions.add(db_transaction)
                return db_attachement

    def get_all_transactions(self):
        contacts = self.get_all_contacts()
        transactions = self.fetch_all_transaction()

        for iban, transactions in transactions.items():
            for transaction in transactions:
                try:
                    tr_db = Transaction.objects.get(
                        uuid=transaction.get('id'),
                        transaction_id=transaction.get('transaction_id'),
                        iban=iban
                    )
                    # TODO: Update ?
                except Transaction.DoesNotExist:
                    category = Category.objects.get_or_create(name=transaction.get('type'))[0]
                    side = 'C' if transaction.get('side') == 'credit' else 'D'

                    initiator = transaction.get('initiator_id')
                    if initiator:
                        initiator = contacts.get(uuid=initiator)

                    tr_db = Transaction.objects.create(
                        uuid=transaction.get('id'),
                        transaction_id=transaction.get('transaction_id'),
                        side=side,
                        iban=iban,
                        emitted_at=transaction.get('emitted_at'),
                        status=transaction.get('status'),
                        amount_cents=transaction.get('amount_cents', 0),
                        currency=transaction.get('currency', 'EUR'),
                        note=transaction.get('note'),
                        label=transaction.get('label'),
                        vat_amount_cents=transaction.get('vat_amount_cents', 0),
                        vat_amount=transaction.get('vat_amount', 0),
                        initiator=initiator,
                        card_last_digits=transaction.get('card_last_digits'),
                        category=category,
                    )

                    for label_qonto in transaction.get('label_ids', []):
                        label_db = Label.objects.get(uuid=label_qonto)
                        tr_db.label_ids.add(label_db)

                    # On valide et raffraichi depuis la db, paske sinon les valeurs plus haut sont toujours des strings...
                    tr_db.refresh_from_db()
                    for attachment_id in transaction.get('attachment_ids', []):
                        self.download_or_update_attachment(attachment_id, tr_db)

        # On va chercher les external transfers liés aux transactions
        external_transferts = self.get_all_external_transfers()

        return Transaction.objects.all()

    def get_all_labels(self):

        labels_qonto = self._get_request_api("labels")
        labels = labels_qonto.get('labels')

        # On crée les labels qui n'ont pas de parent en premier
        parents = [label for label in labels if not label.get('parent_id')]
        for label in parents:
            labeldb, created = Label.objects.get_or_create(
                uuid=label.get('id'),
                name=label.get('name'),
            )

        # On crée les labels qui ont un parent
        childs = [label for label in labels if label.get('parent_id')]
        for label in childs:
            labeldb, created = Label.objects.get_or_create(
                uuid=label.get('id'),
                name=label.get('name'),
            )

            label_parent = Label.objects.get(uuid=label.get('parent_id'))
            labeldb.parent = label_parent
            labeldb.save()

        return LabelsSerializer(Label.objects.all())
