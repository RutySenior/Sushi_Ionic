import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SushiService {
  private apiUrl = 'https://turbo-sniffle-g4x9jwjqg499c9vvw-5000.app.github.dev/api';

  constructor(private http: HttpClient) { }

  getMenu(): Observable<any> {
    return this.http.get(`${this.apiUrl}/menu`);
  }

  inviaOrdine(ordine: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/ordina`, ordine);
  }

  getStatoTavolo(codiceTavolo: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/stato-tavolo/${codiceTavolo}`);
  }
}