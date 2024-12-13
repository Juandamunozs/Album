import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environment/environment';

@Injectable({
  providedIn: 'root'
})
export class FileUploadService {

  private apiUrl = environment.apiUrl;

  private token = localStorage.getItem('token');

  constructor(private http: HttpClient) { }

  uploadFile(formData: FormData): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${this.token}`
    });

    console.log('token enviado:', this.token);

    return this.http.post(this.apiUrl + '/upload', formData, { headers });
  }

  login(usuario: any, contrasena: any): Observable<any> {

    const loginData = { username: usuario, password: contrasena };

    return this.http.post(this.apiUrl + '/login', loginData);
  }

}