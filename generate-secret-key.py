from django.core.signing import Signer
signer = Signer()
sign_string = input("Input something: ")
value = signer.sign(sign_string)
print(value)
