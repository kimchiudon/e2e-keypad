import JSEncrypt from "jsencrypt";

export function encryptHashArray(hashArray: string[], publicKey: string): string | false {
  const combinedHash = hashArray.join("|");

  const encrypt = new JSEncrypt();
  encrypt.setPublicKey(publicKey);

  return encrypt.encrypt(combinedHash);
}