import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../domain/entities/product.dart';
import '../../domain/repositories/product_repository.dart';
import 'product_repository_provider.dart';

class ProductSearchState {
  final bool isLoading;
  final List<Product>? products;
  final String? error;

  ProductSearchState({
    this.isLoading = false,
    this.products,
    this.error,
  });

  ProductSearchState copyWith({
    bool? isLoading,
    List<Product>? products,
    String? error,
  }) {
    return ProductSearchState(
      isLoading: isLoading ?? this.isLoading,
      products: products ?? this.products,
      error: error,
    );
  }
}

class ProductSearchNotifier extends Notifier<ProductSearchState> {
  @override
  ProductSearchState build() {
    return ProductSearchState();
  }

  Future<void> searchProduct(String url) async {
    if (url.trim().isEmpty) {
      state = state.copyWith(error: 'Please enter a valid URL');
      return;
    }

    state = ProductSearchState(isLoading: true);

    try {
      final repository = ref.read(productRepositoryProvider);
      final products = await repository.searchProduct(url);
      state = ProductSearchState(products: products);
    } catch (e) {
      state = ProductSearchState(error: e.toString());
    }
  }

  void clearResults() {
    state = ProductSearchState();
  }
}

final productSearchProvider =
    NotifierProvider<ProductSearchNotifier, ProductSearchState>(() {
  return ProductSearchNotifier();
});
