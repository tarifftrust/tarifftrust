/**
 * The US import duty of a product, in a Google Sheets cell:
 *   =TARIFFTRUST_DUTY("6109.10.00.12", "CN", 10000)
 *
 * In the spreadsheet: Extensions > Apps Script, paste this file, then under Project Settings add the
 * script property TARIFFTRUST_API_KEY with your API key.
 *
 * @param {string} hts The HTS code of the goods.
 * @param {string} origin The country of origin, as two letters.
 * @param {number} customsValue The customs value in US dollars.
 * @return {number|string} The estimated duty; a sentence when it is unknown, never 0.
 * @customfunction
 */
function TARIFFTRUST_DUTY(hts, origin, customsValue) {
  const key = PropertiesService.getScriptProperties().getProperty("TARIFFTRUST_API_KEY");
  if (!key) throw new Error("Add the script property TARIFFTRUST_API_KEY");
  if (customsValue === "" || customsValue == null) throw new Error("The customs value is empty");
  const body = JSON.stringify({
    hts: String(hts),
    origin: String(origin),
    customs_value: String(customsValue),
  });
  const response = UrlFetchApp.fetch("https://api.tarifftrust.com/v1/estimates", {
    method: "post",
    contentType: "application/json",
    headers: {
      Authorization: "Bearer " + key,
      // The same cell recalculated on the same day counts once in your quota.
      "Idempotency-Key": idempotencyKey_(body),
    },
    payload: body,
    muteHttpExceptions: true,
  });
  const answer = JSON.parse(response.getContentText());
  if (response.getResponseCode() !== 200) {
    const error = answer.error || {};
    const fields = error.fields ? " (" + error.fields.join(", ") + ")" : "";
    throw new Error((error.message || "TariffTrust refused the request") + fields);
  }
  if (answer.estimated_duty === null) {
    return "Unknown (" + answer.status + ")";
  }
  return Number(answer.estimated_duty);
}

function idempotencyKey_(body) {
  const today = new Date().toISOString().slice(0, 10);
  const digest = Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, today + body);
  return "sheets-" + digest.map((byte) => ((byte + 256) % 256).toString(16).padStart(2, "0")).join("");
}
