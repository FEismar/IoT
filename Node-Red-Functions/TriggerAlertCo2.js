let co2 = global.get("co2") || 0;
if (msg.payload - co2 >= 100) {
  global.set("co2", msg.payload);
  global.set("lueften_co2", true);
  return {
    payload: {
      chatId: 271097462,
      type: "message",
      content: "CO2 zu hoch! (>1200)",
    },
  };
}
