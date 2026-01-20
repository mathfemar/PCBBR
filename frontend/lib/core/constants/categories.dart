class PCBRCategories {
  static const String cpu = 'CPU';
  static const String cpuCooler = 'CPU Cooler';
  static const String motherboard = 'Motherboard';
  static const String memory = 'Memory';
  static const String storage = 'Storage';
  static const String videoCard = 'Video Card';
  static const String case_ = 'Case';
  static const String powerSupply = 'Power Supply';
  static const String monitor = 'Monitor';
  
  static const List<String> all = [
    cpu,
    cpuCooler,
    motherboard,
    memory,
    storage,
    videoCard,
    case_,
    powerSupply,
    monitor,
  ];
  
  static String getDisplayName(String category) {
    return category;
  }
}
