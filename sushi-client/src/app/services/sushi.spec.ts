import { TestBed } from '@angular/core/testing';

import { Sushi } from './sushi';

describe('Sushi', () => {
  let service: Sushi;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Sushi);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
