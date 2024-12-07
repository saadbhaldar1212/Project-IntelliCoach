import 'dart:developer';

import 'package:mongo_dart/mongo_dart.dart';

class MongoDatabase {
  static const mongoURL =
      "mongodb+srv://dba-fitness-chatbot:jsir0BaNzBuCkyhp@db-fitness-chatbot.tjkkg.mongodb.net/?retryWrites=true&w=majority&appName=db-fitness-chatbot";

  static connect() async {
    var db = await Db.create(mongoURL);
    await db.open();
    inspect(db);
  }
}
