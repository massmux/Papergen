import gnupg


def enc_data(fname, odata, recipient):
    """ encrypts odata to recipient key and writes an armored file. Returns (ok, gpg status) """
    gpg = gnupg.GPG()
    enc_obj = gpg.encrypt(odata, recipient, armor=True)
    if enc_obj.ok:
        with open(fname, 'w') as f:
            f.write(str(enc_obj))
    return enc_obj.ok, enc_obj.status
