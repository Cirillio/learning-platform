// ---------------------------------------------------------------------------
// Filters
// ---------------------------------------------------------------------------

export interface FilterOption {
  value: string;
  label: string;
}

export interface FilterGroup {
  value: string;
  label: string;
  values: FilterOption[];
}

export interface FiltersResponse {
  filters: FilterGroup[];
}

export interface PaginationParams {
  page?: number;
  page_size?: number;
}

export interface CourseFilters extends PaginationParams {
  category?: string;
  difficulty?: string;
  status?: string;
  search?: string;
  ordering?: string;
}
