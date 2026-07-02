import '../models/user_model.dart';
import '../models/auth_response.dart';
import 'api_client.dart';

class AuthService {
  final ApiClient apiClient;

  AuthService(this.apiClient);

  // Register a new user
  Future<UserModel> register({
    required String name,
    required String email,
    required String password,
  }) async {
    try {
      final response = await apiClient.dio.post(
        '/register',
        data: {
          'name': name,
          'email': email,
          'password': password,
        },
      );
      return UserModel.fromJson(response.data as Map<String, dynamic>);
    } catch (e) {
      throw Exception(ApiClient.getErrorMessage(e));
    }
  }

  // Log in user and get token
  Future<AuthResponse> login({
    required String email,
    required String password,
  }) async {
    try {
      final response = await apiClient.dio.post(
        '/login',
        data: {
          'email': email,
          'password': password,
        },
      );
      return AuthResponse.fromJson(response.data as Map<String, dynamic>);
    } catch (e) {
      throw Exception(ApiClient.getErrorMessage(e));
    }
  }

  // Fetch current logged-in user profile details (/me)
  Future<UserModel> fetchMe() async {
    try {
      final response = await apiClient.dio.get('/me');
      return UserModel.fromJson(response.data as Map<String, dynamic>);
    } catch (e) {
      throw Exception(ApiClient.getErrorMessage(e));
    }
  }
}
