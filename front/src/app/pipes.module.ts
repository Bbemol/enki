import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FilterStatusPipe } from './evenements/liste-evenements/filter-status.pipe';
import { HighlightIncludedCharsPipe } from './highlight-included-chars.pipe';



@NgModule({
  declarations: [
    FilterStatusPipe,
    HighlightIncludedCharsPipe,
  ],
  exports: [
    FilterStatusPipe,
    HighlightIncludedCharsPipe,
  ],
  imports: [
    CommonModule
  ]
})
export class PipesModule { }
