import '../../domain/entities/product.dart';

class ProductModel extends Product {
  ProductModel({
    super.name,
    super.price,
    required super.url,
    super.store,
    super.error,
  });

  factory ProductModel.fromJson(Map<String, dynamic> json) {
    return ProductModel(
      name: json['name'] as String?,
      price: json['price'] != null ? (json['price'] as num).toDouble() : null,
      url: json['url'] as String,
      store: json['store'] as String?,
      error: json['error'] as String?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'name': name,
      'price': price,
      'url': url,
      'store': store,
      'error': error,
    };
  }
}
