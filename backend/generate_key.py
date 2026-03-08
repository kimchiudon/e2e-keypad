from Crypto.PublicKey import RSA

key = RSA.generate(2048)

private_key = key.export_key().decode("utf-8")
public_key = key.publickey().export_key().decode("utf-8")

print("=== PUBLIC KEY ===")
print(public_key)

print("\n=== PRIVATE KEY ===")
print(private_key)