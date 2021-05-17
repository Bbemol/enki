import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { DetailMessageComponent } from './detail-message.component';

describe('DetailMessageComponent', () => {
  let component: DetailMessageComponent;
  let fixture: ComponentFixture<DetailMessageComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ DetailMessageComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DetailMessageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

/*   it('should create', () => {
    expect(component).toBeTruthy();
  }); */
});
