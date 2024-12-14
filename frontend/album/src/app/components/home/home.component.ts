import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { NavegationComponent } from "../navegation/navegation.component";
import { FileUploadService } from '../../service/file-upload.service';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, NavegationComponent, HttpClientModule],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
})
export class HomeComponent implements OnInit {
  photos: string[] = [];

  constructor(private fileUploadService: FileUploadService) { }

  ngOnInit(): void {
    this.loadImages();
  }

  // Método para cargar las imágenes
  loadImages(): void {
    this.fileUploadService.getImages().subscribe({
      next: (response) => {
        this.photos = response.images;
        console.log('Fotos cargadas:', this.photos);
      },
      error: (err) => {
        console.error('Error al cargar las imágenes:', err);
      },
    });
  }

  // Método para eliminar una imagen
  eliminar(photo: string): void {
    console.log('Eliminar:', photo);
    const imageName = photo.split('/uploads/')[1]; 
  
    if (imageName) {
      console.log('Nombre de la imagen a eliminar:', imageName);
  
      this.fileUploadService.deleteImage(imageName).subscribe(
        (response) => {
          console.log('Imagen eliminada con éxito:', response);
          this.loadImages();
        },
        (error) => {
          console.error('Error al eliminar la imagen:', error);
        }
      );
    } else {
      console.error('No se pudo obtener el nombre de la imagen desde la URL.');
    }
  }
}

