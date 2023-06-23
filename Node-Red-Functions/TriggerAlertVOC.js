let voc = global.get("voc") || 0;
if (msg.payload - voc >= 100) {
  global.set("voc", msg.payload);
  global.set("lueften_voc", true);
  return {
    payload: {
      chatId: 271097462,
      type: "message",
      content: "VOC zu hoch! (>1300)",
    },
  };
}
