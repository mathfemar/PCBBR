class ApiConstants {
  static const String baseUrl = 'http://localhost:8000';
  static const String searchEndpoint = '/search';
  
  static String getSearchUrl(String productUrl) {
    return '$baseUrl$searchEndpoint?url=$productUrl';
  }
}
