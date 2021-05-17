import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { interval, Observable, of, Subject, throwError } from 'rxjs';
import { catchError, debounce, pluck, switchMap } from 'rxjs/operators';
import { environment } from 'src/environments/environment';
import { HTTP_DATA, SEARCH_MIN_CHARS } from '../constants/constants';
import { SearchLocationService } from './search-location.service';
import { Location } from 'src/app/interfaces';
import { HighlightIncludedCharsPipe } from '../highlight-included-chars.pipe';

@Component({
  selector: 'app-search-location',
  templateUrl: './search-location.component.html',
  styleUrls: ['./search-location.component.scss'],
  providers: [HighlightIncludedCharsPipe]
})
export class SearchLocationComponent implements OnInit {

  locationSearch = new FormControl('', Validators.required);
  subject = new Subject();
  locationResults$: Observable<Location[]>;
  locationResults: Location[];
  groupType: string;


  constructor(
    private http: HttpClient,
    private route: ActivatedRoute,
    private router: Router,
    private searchLocationService: SearchLocationService,
    private highlightTransform: HighlightIncludedCharsPipe,
  ) {

    this.groupType = this.route.snapshot.queryParams.groupType

    this.locationResults$ = this.subject.pipe(
      debounce(() => interval(500)),
      switchMap((inputValue: string) => {
        return this.http.get<any>(`${environment.backendUrl}/locations?query=${inputValue}`).pipe(
          pluck(HTTP_DATA),
          catchError((error) => {
            if (error.status === 404) {
              return of([])
            } else {
              console.error(error)
              return throwError(
                'Something bad happened; please try again later.');
            }
          })
        )
      })
    );

    this.locationResults$.subscribe((results) => {
      this.locationResults = results
    });

    this.locationSearch.valueChanges.subscribe((value: string) => {
      if (value.length >= SEARCH_MIN_CHARS) {
        this.subject.next(value)
      }
    });
  }

  getLocationInfos(location: Location, searchvalue: string): string {
    const label = this.highlightTransform.transform(location.label, searchvalue)
    const external_id = this.highlightTransform.transform(location.external_id, searchvalue)
    return `${label} (${external_id})`
  }

  ngOnInit(): void {
  }

  selectLocation(location: Location): void {
    this.searchLocationService.setSelectedLocation(location)
    this.router.navigate([`..`], {relativeTo: this.route})
  }

}
