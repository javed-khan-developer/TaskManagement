import 'package:flutter/material.dart';
import '../models/task_model.dart';
import '../services/task_service.dart';

class TaskProvider extends ChangeNotifier {
  final TaskService _taskService;

  List<TaskModel> _tasks = [];
  bool _isLoading = false;
  String? _errorMessage;
  String? _successMessage;

  // Search and filter fields
  String _searchQuery = '';
  String _statusFilter = 'All'; // 'All', 'Pending', 'Completed'

  TaskProvider(this._taskService);

  List<TaskModel> get tasks => _tasks;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;
  String? get successMessage => _successMessage;
  String get searchQuery => _searchQuery;
  String get statusFilter => _statusFilter;

  // Perform client-side filter and search in-memory
  List<TaskModel> get filteredTasks {
    return _tasks.where((task) {
      // 1. Filter by status
      final matchStatus = _statusFilter == 'All' || 
          task.status.toLowerCase() == _statusFilter.toLowerCase();

      // 2. Filter by search query (title or description)
      final matchSearch = _searchQuery.isEmpty ||
          task.title.toLowerCase().contains(_searchQuery.toLowerCase()) ||
          task.description.toLowerCase().contains(_searchQuery.toLowerCase());

      return matchStatus && matchSearch;
    }).toList();
  }

  void clearMessages() {
    _errorMessage = null;
    _successMessage = null;
    notifyListeners();
  }

  void setSearchQuery(String query) {
    _searchQuery = query;
    notifyListeners();
  }

  void setStatusFilter(String filter) {
    _statusFilter = filter;
    notifyListeners();
  }

  // Fetch all tasks for current user
  Future<void> fetchTasks() async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      _tasks = await _taskService.getTasks();
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _errorMessage = e.toString().replaceFirst('Exception: ', '');
      _isLoading = false;
      notifyListeners();
    }
  }

  // Create a new task
  Future<bool> createTask(String title, String description) async {
    _isLoading = true;
    _errorMessage = null;
    _successMessage = null;
    notifyListeners();

    try {
      final newTask = await _taskService.createTask(title, description);
      _tasks.insert(0, newTask); // Add to the top of list
      _successMessage = 'Task created successfully!';
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

  // Update a task details & status
  Future<bool> updateTask({
    required int id,
    required String title,
    required String description,
    required String status,
  }) async {
    _isLoading = true;
    _errorMessage = null;
    _successMessage = null;
    notifyListeners();

    try {
      final updatedTask = await _taskService.updateTask(
        id: id,
        title: title,
        description: description,
        status: status,
      );

      // Replace task in memory list
      final index = _tasks.indexWhere((t) => t.id == id);
      if (index != -1) {
        _tasks[index] = updatedTask;
      }
      
      _successMessage = 'Task updated successfully!';
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

  // Toggle status shortcut
  Future<bool> toggleTaskStatus(TaskModel task) async {
    final newStatus = task.status.toLowerCase() == 'completed' ? 'Pending' : 'Completed';
    // Optimistic UI update
    final index = _tasks.indexWhere((t) => t.id == task.id);
    final originalTask = _tasks[index];
    _tasks[index] = task.copyWith(status: newStatus);
    notifyListeners();

    try {
      final updated = await _taskService.updateTask(
        id: task.id,
        title: task.title,
        description: task.description,
        status: newStatus,
      );
      _tasks[index] = updated;
      notifyListeners();
      return true;
    } catch (e) {
      // Revert on error
      _tasks[index] = originalTask;
      _errorMessage = e.toString().replaceFirst('Exception: ', '');
      notifyListeners();
      return false;
    }
  }

  // Delete a task
  Future<bool> deleteTask(int id) async {
    _isLoading = true;
    _errorMessage = null;
    _successMessage = null;
    notifyListeners();

    // Store in case we want to undo or fallback
    final index = _tasks.indexWhere((t) => t.id == id);
    if (index == -1) return false;
    final deletedTask = _tasks[index];

    // Optimistic UI deletion
    _tasks.removeAt(index);
    notifyListeners();

    try {
      await _taskService.deleteTask(id);
      _successMessage = 'Task deleted successfully!';
      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      // Revert if API fails
      _tasks.insert(index, deletedTask);
      _errorMessage = e.toString().replaceFirst('Exception: ', '');
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }
}
