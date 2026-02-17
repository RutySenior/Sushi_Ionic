import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class StaffService {
  private apiUrl = 'https://turbo-sniffle-g4x9jwjqg499c9vvw-5000.app.github.dev/api';

  constructor(private http: HttpClient) { }

  // Gestione Ordini
  getTuttiOrdini(): Observable<any> {
    return this.http.get(`${this.apiUrl}/staff/ordini`);
  }

  aggiornaStato(id_ordine: number, nuovo_stato: string): Observable<any> {
    return this.http.patch(`${this.apiUrl}/staff/ordine-stato`, { id_ordine, nuovo_stato });
  }

  // Gestione Menu (CRUD)
  getMenu(): Observable<any> {
    return this.http.get(`${this.apiUrl}/menu`);
  }

  getCategorie(): Observable<any> {
    return this.http.get(`${this.apiUrl}/categorie`);
  }

  aggiungiProdotto(prodotto: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/staff/menu`, prodotto);
  }

  eliminaProdotto(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/staff/menu/${id}`);
  }
}