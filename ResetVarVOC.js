if (global.get("lueften_voc") == true) {
  global.set("lueften_voc", false);
  global.set("voc", 0);
  return {
    payload: {
      chatId: 271097462,
      type: "message",
      content:
        "Glückwunsch du hast es geschafft die Luftqualität zu verbessern! (VOC)",
    },
  };
}
