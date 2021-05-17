import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'highlightIncludedChars'
})
export class HighlightIncludedCharsPipe implements PipeTransform {

  transform(value: string, searchValue: string): unknown {
    const indexOfSearchValue = value.toLowerCase().indexOf(searchValue.toLowerCase())
    const slicedValue = value.slice(indexOfSearchValue, indexOfSearchValue + searchValue.length)
    return indexOfSearchValue !== -1 ? value.replace(slicedValue, `<span class="-emphasize">${slicedValue}</span>`) : value;
  }

}
