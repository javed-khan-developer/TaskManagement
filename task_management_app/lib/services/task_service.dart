import '../models/task_model.dart';
import 'api_client.dart';

class TaskService {
  final ApiClient apiClient;

  TaskService(this.apiClient);

  // List all tasks of logged-in user
  Future<List<TaskModel>> getTasks() async {
    try {
      final response = await apiClient.dio.get('/tasks/');
      final data = response.data as List;
      return data.map((json) => TaskModel.fromJson(json as Map<String, dynamic>)).toList();
    } catch (e) {
      throw Exception(ApiClient.getErrorMessage(e));
    }
  }

  // Get a single task details
  Future<TaskModel> getTask(int id) async {
    try {
      final response = await apiClient.dio.get('/tasks/$id');
      return TaskModel.fromJson(response.data as Map<String, dynamic>);
    } catch (e) {
      throw Exception(ApiClient.getErrorMessage(e));
    }
  }

  // Create a new task
  Future<TaskModel> createTask(String title, String description) async {
    try {
      final response = await apiClient.dio.post(
        '/tasks/',
        data: {
          'title': title,
          'description': description,
        },
      );
      return TaskModel.fromJson(response.data as Map<String, dynamic>);
    } catch (e) {
      throw Exception(ApiClient.getErrorMessage(e));
    }
  }

  // Update an existing task
  Future<TaskModel> updateTask({
    required int id,
    required String title,
    required String description,
    required String status,
  }) async {
    try {
      final response = await apiClient.dio.put(
        '/tasks/$id',
        data: {
          'title': title,
          'description': description,
          'status': status,
        },
      );
      return TaskModel.fromJson(response.data as Map<String, dynamic>);
    } catch (e) {
      throw Exception(ApiClient.getErrorMessage(e));
    }
  }

  // Delete a task
  Future<void> deleteTask(int id) async {
    try {
      await apiClient.dio.delete('/tasks/$id');
    } catch (e) {
      throw Exception(ApiClient.getErrorMessage(e));
    }
  }
}
