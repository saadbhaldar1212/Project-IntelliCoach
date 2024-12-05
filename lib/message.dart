class Message {
  bool isSender;
  String msg;
  String? errorMsg;

  Message({
    required this.isSender,
    required this.msg,
    this.errorMsg,
  });
}
