import gnupg

gpg = gnupg.GPG()


def enc_data(fname, odata, recipient):
    enc_obj = gpg.encrypt(odata, recipient)
    if enc_obj.ok:
        with open(fname, 'w') as f:
            f.write(str(enc_obj))
    return enc_obj.ok
