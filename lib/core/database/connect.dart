import 'dart:developer';

import 'package:mongo_dart/mongo_dart.dart';

class MongoDatabase {
  static const MONGO_URL =
      "mongodb+srv://dba-fitness-chatbot:jsir0BaNzBuCkyhp@db-fitness-chatbot.tjkkg.mongodb.net/?retryWrites=true&w=majority&appName=db-fitness-chatbot";
  static const COLLECTION_NAME = "users";

  static connect() async {
    var db = await Db.create(MONGO_URL);
    await db.open();
    inspect(db);
    var collection = db.collection(COLLECTION_NAME);
    print(collection.collectionName);
  }
}
