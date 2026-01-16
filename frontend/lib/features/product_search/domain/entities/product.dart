class Product {
  final String? name;
  final double? price;
  final String url;
  final String? store;
  final String? error;

  Product({
    this.name,
    this.price,
    required this.url,
    this.store,
    this.error,
  });

  bool get hasError => error != null;
  bool get isValid => name != null && price != null;
}
