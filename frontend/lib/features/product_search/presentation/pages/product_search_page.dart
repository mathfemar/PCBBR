import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../providers/product_search_provider.dart';
import '../widgets/product_card.dart';

class ProductSearchPage extends ConsumerStatefulWidget {
  const ProductSearchPage({super.key});

  @override
  ConsumerState<ProductSearchPage> createState() => _ProductSearchPageState();
}

class _ProductSearchPageState extends ConsumerState<ProductSearchPage> {
  final _urlController = TextEditingController();
  final _formKey = GlobalKey<FormState>();

  @override
  void dispose() {
    _urlController.dispose();
    super.dispose();
  }

  void _onSearch() {
    if (_formKey.currentState!.validate()) {
      ref.read(productSearchProvider.notifier).searchProduct(_urlController.text);
    }
  }

  @override
  Widget build(BuildContext context) {
    final searchState = ref.watch(productSearchProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('PCBBR - Busca de Preços'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Form(
                  key: _formKey,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      Text(
                        'Cole a URL do produto',
                        style: Theme.of(context).textTheme.titleMedium,
                      ),
                      const SizedBox(height: 12),
                      TextFormField(
                        controller: _urlController,
                        decoration: const InputDecoration(
                          hintText: 'https://www.exemplo.com.br/produto',
                          prefixIcon: Icon(Icons.link),
                        ),
                        validator: (value) {
                          if (value == null || value.trim().isEmpty) {
                            return 'Por favor, insira uma URL';
                          }
                          if (!value.startsWith('http')) {
                            return 'URL inválida';
                          }
                          return null;
                        },
                        onFieldSubmitted: (_) => _onSearch(),
                      ),
                      const SizedBox(height: 16),
                      ElevatedButton.icon(
                        onPressed: searchState.isLoading ? null : _onSearch,
                        icon: searchState.isLoading
                            ? const SizedBox(
                                width: 20,
                                height: 20,
                                child: CircularProgressIndicator(
                                  strokeWidth: 2,
                                ),
                              )
                            : const Icon(Icons.search),
                        label: Text(
                          searchState.isLoading ? 'Buscando...' : 'Buscar Preço',
                        ),
                        style: ElevatedButton.styleFrom(
                          padding: const EdgeInsets.symmetric(vertical: 16),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
            const SizedBox(height: 24),
            if (searchState.error != null)
              Card(
                color: Colors.red.shade50,
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Row(
                    children: [
                      Icon(Icons.error_outline, color: Colors.red.shade700),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Text(
                          searchState.error!,
                          style: TextStyle(color: Colors.red.shade700),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            if (searchState.products != null && searchState.products!.isNotEmpty)
              Expanded(
                child: ListView.builder(
                  itemCount: searchState.products!.length,
                  itemBuilder: (context, index) {
                    return ProductCard(
                      product: searchState.products![index],
                    );
                  },
                ),
              ),
            if (searchState.products != null &&
                searchState.products!.isEmpty &&
                !searchState.isLoading)
              const Expanded(
                child: Center(
                  child: Text('Nenhum produto encontrado'),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
