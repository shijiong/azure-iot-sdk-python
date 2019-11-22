from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from OpenSSL import crypto
from datetime import datetime, timedelta, time
import uuid
import os
import argparse
import getpass

# one_day = datetime.timedelta(1, 0, 0)
PUBLIC_EXPONENT = 65537


def create_certificate_chain(
    common_name,
    ca_password,
    intermediate_password,
    device_password,
    device_count=1,
    key_size=4096,
    days=365,
):
    """
    This method will create a basic 3 layered chain certificate containing a root, then an intermediate and then some number of leaf certificates.
    This function is only used when the certificates are created from script.

    :param common_name: The common name to be used in the subject. This is a single common name which would be applied to all certs created. Since this common name is meant for all,
    this common name will be prepended by the words "root", "inter" and "device" for root, intermediate and device certificates.
    For device certificates the common name will be further appended with the index of the device.
    :param ca_password: The password for the root certificate which is going to be referenced by the intermediate.
    :param intermediate_password: The password for the intermediate certificate
    :param device_password: The password for the device certificate
    :param device_count: The number of leaf devices for which that many number of certificates will be generated.
    :param key_size: The key size to use for encryption. The default is 4096.
    :param days: The number of days for which the certificate is valid. The default is 1 year or 365 days.
    For the root cert this value is multiplied by 10. For the device certificates this number will be divided by 10.
    """
    common_name_for_root = "root" + common_name
    create_root_ca(
        common_name=common_name_for_root, ca_password=ca_password, key_size=key_size, days=days * 10
    )  # Arg parse password


def create_private_key(password_file, password=None, key_size=4096):
    private_key = rsa.generate_private_key(
        public_exponent=PUBLIC_EXPONENT, key_size=key_size, backend=default_backend()
    )
    # Write our key to file
    with open(password_file, "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.BestAvailableEncryption(str.encode(password)),
            )
        )
    return private_key


def create_root_ca(root_common_name, root_private_key, days=3650):
    file_root_certificate = "demoCACrypto/newcerts/ca_cert.pem"

    root_public_key = root_private_key.public_key()

    builder = x509.CertificateBuilder()
    builder = create_ca_type_cert(builder, root_common_name, root_public_key, days)

    root_cert = builder.sign(
        private_key=root_private_key, algorithm=hashes.SHA256(), backend=default_backend()
    )
    with open(file_root_certificate, "wb") as f:
        f.write(root_cert.public_bytes(serialization.Encoding.PEM))

    return root_cert


def create_intermediate_ca(root_cert, root_key, intermediate_csr, days=3650):
    file_intermediate_certificate = "demoCACrypto/newcerts/intermediate_cert.pem"

    intermediate_csr_crypto = crypto.X509Req.from_cryptography(intermediate_csr)
    root_cert_crypto = crypto.X509.from_cryptography(root_cert)
    root_key_crypto = crypto.PKey.from_cryptography_key(root_key)

    intermediate_cert_crypto = crypto.X509()
    intermediate_cert_crypto.set_serial_number(int(uuid.uuid4()))
    intermediate_cert_crypto.add_extensions(intermediate_csr_crypto.get_extensions())
    intermediate_cert_crypto.gmtime_adj_notBefore(0)
    intermediate_cert_crypto.gmtime_adj_notAfter(60 * 60 * 24 * int(days / 10))
    intermediate_cert_crypto.set_issuer(root_cert_crypto.get_subject())
    intermediate_cert_crypto.set_subject(intermediate_csr_crypto.get_subject())
    intermediate_cert_crypto.set_pubkey(intermediate_csr_crypto.get_pubkey())
    intermediate_cert_crypto.sign(root_key_crypto, "sha256")

    with open(file_intermediate_certificate, "wb") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, intermediate_cert_crypto))

    intermediate_cert = intermediate_cert_crypto.to_cryptography()
    return intermediate_cert

    # builder = x509.CertificateBuilder()
    # builder = create_ca_type_cert(builder, intermediate_common_name, intermediate_public_key, days)
    #
    # certificate = builder.sign(
    #     private_key=intermediate_private_key, algorithm=hashes.SHA256(),
    #     backend=default_backend()
    # )
    # with open(file_intermediate_certificate, "wb") as f:
    #     f.write(certificate.public_bytes(serialization.Encoding.PEM))


def create_csr(password_file, csr_file, common_name, password=None, key_size=4096):
    intermediate_private_key = create_private_key(
        password_file=password_file, password=password, key_size=key_size
    )
    builder = (
        x509.CertificateSigningRequestBuilder()
        .subject_name(
            x509.Name(
                [
                    # Provide various details about who we are.
                    x509.NameAttribute(NameOID.COMMON_NAME, str.encode(common_name).decode("utf-8"))
                ]
            )
        )
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=False)
    )

    csr = builder.sign(
        private_key=intermediate_private_key, algorithm=hashes.SHA256(), backend=default_backend()
    )

    with open(csr_file, "wb") as f:
        f.write(csr.public_bytes(serialization.Encoding.PEM))

    return csr


def create_ca_type_cert(builder, common_name, public_key, days):

    builder = builder.subject_name(
        x509.Name(
            [
                x509.NameAttribute(
                    NameOID.COMMON_NAME, str.encode(common_name).decode("utf-8")
                )  # unicode(common_name, "utf-8")
            ]
        )
    )
    builder = builder.issuer_name(
        x509.Name(
            [x509.NameAttribute(NameOID.COMMON_NAME, str.encode(common_name).decode("utf-8"))]
        )
    )
    builder = builder.not_valid_before(datetime.today())
    builder = builder.not_valid_after(datetime.today() + timedelta(days=days))
    builder = builder.serial_number(int(uuid.uuid4()))
    builder = builder.add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
    return builder.public_key(public_key)


def create_certificate_from_csr(req, issuer_cert, issuer_key, serial, not_before, not_after):
    """
    Generate a certificate given a certificate request.
    Arguments: req        - Certificate reqeust to use
               issuerCert - The certificate of the issuer
               issuerKey  - The private key of the issuer
               serial     - Serial number for the certificate
               notBefore  - Timestamp (relative to now) when the certificate
                            starts being valid
               notAfter   - Timestamp (relative to now) when the certificate
                            stops being valid
               digest     - Digest method to use for signing, default is md5
    Returns:   The signed certificate in an X509 object
    """
    # cert = crypto.X509()
    # cert.set_serial_number(serial)
    # cert.gmtime_adj_notBefore(not_before)
    # cert.gmtime_adj_notAfter(not_after)
    # cert.set_issuer(issuer_cert.get_subject())
    # cert.set_subject(req.get_subject())
    # cert.set_pubkey(req.get_pubkey())
    # cert.sign(issuer_key, digest)
    # return cert
    pass


def create_directories_and_prereq_files(pipeline):
    """
    This function creates the necessary directories and files. This needs to be called as the first step before doing anything.
    :param pipeline: The boolean representing if function has been called from pipeline or not. True for pipeline, False for calling like a script.
    """
    os.system("mkdir demoCACrypto")
    if pipeline:
        # This command does not work when we run locally. So we have to pass in the pipeline variable
        os.system("touch demoCACrypto/index.txt")
    else:
        os.system("type nul > demoCACrypto/index.txt")
        # TODO Do we need this
        # os.system("type nul > demoCACrypto/index.txt.attr")

    os.system("echo 1000 > demoCACrypto/serial")
    # Create this folder as configuration file makes new keys go here
    os.mkdir("demoCACrypto/private")
    # Create this folder as configuration file makes new certificates go here
    os.mkdir("demoCACrypto/newcerts")


def before_cert_creation_from_pipeline():
    """
    This function creates the required folder and files before creating certificates.
    This also copies an openssl configurtaion file to be used for the generation of this certificates.
    NOTE : This function is only applicable when called from the pipeline via E2E tests
    and need not be used when it is called as a script.
    """
    create_directories_and_prereq_files(True)

    # shutil.copy("config/openssl.cnf", "demoCACrypto/openssl.cnf")
    #
    # if os.path.exists("demoCACrypto/openssl.cnf"):
    #     print("Configuration file have been copied")
    # else:
    #     print("Configuration file have NOT been copied")


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Generate a certificate chain.")
    # parser.add_argument("domain", help="Domain name or common name.")
    #
    # parser.add_argument(
    #     "--ca-password", type=str, help="CA key password. If omitted it will be prompted."
    # )
    #
    # args = parser.parse_args()
    #
    # common_name = args.domain
    # if args.ca_password:
    #     ca_password = args.ca_password
    # else:
    #     ca_password = getpass.getpass("Enter pass phrase for root key: ")

    # common_name = "leviosa"
    # print(common_name.decode("utf-8"))
    # bytes_val = str.encode(common_name)
    # print(bytes_val)
    # u_val = bytes_val.decode("utf-8")
    # print(u_val)
    # print(str.encode(common_name).decode("utf-8"))

    create_directories_and_prereq_files(False)
    abs_common_name = "leviosa"
    root_pass = "hogwarts"
    inter_pass = "hogwartsi"
    root_password_file = "demoCACrypto/private/ca_key.pem"
    root_private_key = create_private_key(
        password_file=root_password_file, password=root_pass, key_size=4096
    )
    root_cert = create_root_ca(
        root_common_name="root" + abs_common_name, root_private_key=root_private_key, days=3650
    )  # Arg parse password

    intermediate_password_file = "demoCACrypto/private/intermediate_key.pem"
    intermediate_csr_file = "demoCA/newcerts/intermediate_csr.pem"
    intermediate_csr = create_csr(
        password_file=intermediate_password_file,
        csr_file=intermediate_csr_file,
        common_name="inter" + abs_common_name,
        password=inter_pass,
        key_size=4096,
    )
    intermediate_cert = create_intermediate_ca(
        root_cert=root_cert, root_key=root_private_key, intermediate_csr=intermediate_csr, days=3650
    )
