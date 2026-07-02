import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/user_model.dart';
import '../services/auth_service.dart';

class AuthProvider extends ChangeNotifier {
  final AuthService _authService;

  UserModel? _currentUser;
  String? _token;
  bool _isLoading = false;
  String? _errorMessage;

  AuthProvider(this._authService);

  UserModel? get currentUser => _currentUser;
  String? get token => _token;
  bool get isAuthenticated => _token != null;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;

  void clearError() {
    _errorMessage = null;
    notifyListeners();
  }

  // Load token from SharedPreferences and fetch current user info
  Future<bool> loadTokenAndFetchUser() async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      final prefs = await SharedPreferences.getInstance();
      final savedToken = prefs.getString('auth_token');

      if (savedToken != null && savedToken.isNotEmpty) {
        _token = savedToken;
        // Verify token by calling /me
        _currentUser = await _authService.fetchMe();
        _isLoading = false;
        notifyListeners();
        return true;
      }
    } catch (e) {
      // Token is invalid/expired or connection issue
      _token = null;
      _currentUser = null;
      final prefs = await SharedPreferences.getInstance();
      await prefs.remove('auth_token');
    }

    _isLoading = false;
    notifyListeners();
    return false;
  }

  // Log in user and fetch profile
  Future<bool> login(String email, String password) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      final authResponse = await _authService.login(email: email, password: password);
      _token = authResponse.accessToken;

      // Save to SharedPreferences
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('auth_token', _token!);

      // Fetch user profile
      _currentUser = await _authService.fetchMe();
      
      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _errorMessage = e.toString().replaceFirst('Exception: ', '');
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  // Register user, then automatically trigger login
  Future<bool> register(String name, String email, String password) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      await _authService.register(name: name, email: email, password: password);
      
      // Auto login on successful register
      final success = await login(email, password);
      return success;
    } catch (e) {
      _errorMessage = e.toString().replaceFirst('Exception: ', '');
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  // Log out user
  Future<void> logout() async {
    _isLoading = true;
    notifyListeners();

    try {
      final prefs = await SharedPreferences.getInstance();
      await prefs.remove('auth_token');
      _token = null;
      _currentUser = null;
    } catch (e) {
      _errorMessage = e.toString().replaceFirst('Exception: ', '');
    }

    _isLoading = false;
    notifyListeners();
  }
}
