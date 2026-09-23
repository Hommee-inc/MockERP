# Databricks notebook source
# MAGIC %md
# MAGIC # Faker Provider

# COMMAND ----------

# MAGIC %md
# MAGIC ## Install dependency

# COMMAND ----------

# MAGIC %pip install Faker

# COMMAND ----------

# MAGIC %md
# MAGIC ## Reset Python environment

# COMMAND ----------

# MAGIC %restart_python

# COMMAND ----------

# MAGIC %md
# MAGIC ## Imports

# COMMAND ----------

# MAGIC %run ./provider_contract

# COMMAND ----------

class FakerProvider(
    NameProvider,
    EmailProvider,
    AddressProvider,
    PhoneProvider,
    DocumentProvider
):

    def __init__(self, locale="pt_BR"):
        self.fake = Faker(locale)

    def name(self):
        return self.fake.name()

    def email(self):
        return self.fake.email()

    def address(self):
        return self.fake.address()

    def phone(self):
        return self.fake.phone_number()

    def document(self, document_type):

        if document_type == "cpf":
            return self.fake.cpf()

        if document_type == "cnpj":
            return self.fake.cnpj()

        raise ValueError(
            f"Unsupported document type: {document_type}"
        )