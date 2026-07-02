import 'dart:typed_data';
import 'package:dio/dio.dart';
import 'package:http_parser/http_parser.dart';
import 'api_client.dart';

class FileService {
  final ApiClient apiClient;

  FileService(this.apiClient);

  // Upload file to the /upload endpoint
  Future<Map<String, dynamic>> uploadFile({
    required Uint8List fileBytes,
    required String filename,
  }) async {
    try {
      final formData = FormData.fromMap({
        'file': MultipartFile.fromBytes(
          fileBytes,
          filename: filename,
          contentType: MediaType('application', 'octet-stream'),
        ),
      });

      final response = await apiClient.dio.post(
        '/upload',
        data: formData,
        options: Options(
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        ),
      );

      return response.data as Map<String, dynamic>;
    } catch (e) {
      throw Exception(ApiClient.getErrorMessage(e));
    }
  }
}
