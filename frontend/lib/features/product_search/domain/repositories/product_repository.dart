import '../entities/product.dart';

abstract class ProductRepository {
  Future<List<Product>> searchProduct(String url);
}
