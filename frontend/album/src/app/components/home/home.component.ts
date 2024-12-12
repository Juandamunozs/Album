import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { NavegationComponent } from "../navegation/navegation.component";
import { uploadDialogComponent } from "../../dialog/upload/upload";

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, NavegationComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {

  photos: string[] = [
    'https://pixum-cms.imgix.net/7G7IULsB6o0iH2D5hR12aO/918d294f9f637bba2bab98408b4b0c01/pfb-quadratisch-klebebindung-hochzeit-hardcover-2024-01.jpg?auto=compress,format&rect=102,726,1946,1095&trim=false',  // Foto 1
    'https://create.vista.com/s3-static/create/uploads/2022/09/free-photo-book-maker-900x891-1.webp',  // Foto 2
    'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQbvTUC2PO3wxJsrtbOt-hK_dNtWY6oQRjCIg&s',  // Foto 3
    'https://consumer-catalog-service-master.storage.googleapis.com/images/FotoLibro_Rivestito-01.original.width-504.format-jpeg.jpegquality-95.jpg',  // Foto 4
    'https://pixum-cms.imgix.net/7G7IULsB6o0iH2D5hR12aO/918d294f9f637bba2bab98408b4b0c01/pfb-quadratisch-klebebindung-hochzeit-hardcover-2024-01.jpg?auto=compress,format&rect=102,726,1946,1095&trim=false',  // Foto 1
    'https://create.vista.com/s3-static/create/uploads/2022/09/free-photo-book-maker-900x891-1.webp',  // Foto 2
    'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQbvTUC2PO3wxJsrtbOt-hK_dNtWY6oQRjCIg&s',  // Foto 3
    'https://consumer-catalog-service-master.storage.googleapis.com/images/FotoLibro_Rivestito-01.original.width-504.format-jpeg.jpegquality-95.jpg',  // Foto 4
    'https://pixum-cms.imgix.net/7G7IULsB6o0iH2D5hR12aO/918d294f9f637bba2bab98408b4b0c01/pfb-quadratisch-klebebindung-hochzeit-hardcover-2024-01.jpg?auto=compress,format&rect=102,726,1946,1095&trim=false',  // Foto 1
    'https://create.vista.com/s3-static/create/uploads/2022/09/free-photo-book-maker-900x891-1.webp',  // Foto 2
    'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQbvTUC2PO3wxJsrtbOt-hK_dNtWY6oQRjCIg&s',  // Foto 3
    'https://consumer-catalog-service-master.storage.googleapis.com/images/FotoLibro_Rivestito-01.original.width-504.format-jpeg.jpegquality-95.jpg',  // Foto 4
  ];
  
  

}
