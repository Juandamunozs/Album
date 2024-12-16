import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environment/environment';

@Injectable({
  providedIn: 'root'
})

export class FileUploadService {

  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  // Método privado para obtener los headers con el token
  private getHeaders(): HttpHeaders {
    const token = localStorage.getItem('token');
    if (!token) {
      console.log('No hay token');
      throw new Error('No hay token');
    }
    return new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });
  }

  // Método para subir el archivo
  uploadFile(formData: FormData): Observable<any> {
    const headers = this.getHeaders();
    console.log('Token enviado:', localStorage.getItem('token'));
    return this.http.post(this.apiUrl + '/save', formData, { headers });
  }

  // Método para hacer login
  login(usuario: any, contrasena: any): Observable<any> {
    const loginData = { username: usuario, password: contrasena };
    return this.http.post(this.apiUrl + '/login', loginData);
  }

  // Método para obtener las imágenes
  getImages(): Observable<{ images: string[] }> {
    const headers = this.getHeaders();
    return this.http.get<{ images: string[] }>(this.apiUrl + '/list', { headers });
  }

  getImageWithToken(imageUrl: string): Observable<Blob> {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('No hay token');
    }

    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);

    return this.http.get(imageUrl, { headers, responseType: 'blob' });
  }

  // Método para eliminar una imagen
  deleteImage(imageName: string): Observable<any> {
    const headers = this.getHeaders();
    return this.http.delete(this.apiUrl + '/delete_image/' + imageName, { headers });
  }
}
