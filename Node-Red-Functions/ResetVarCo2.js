if (global.get("lueften_co2") == true) {
  global.set("lueften_co2", false);
  global.set("co2", 0);
  return {
    payload: {
      chatId: 271097462,
      type: "message",
      content:
        "Glückwunsch du hast es geschafft die Luftqualität zu verbessern! (Co2)",
    },
  };
}
