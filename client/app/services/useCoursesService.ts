import type {
  Category,
  CourseDetail,
  CourseFilters,
  CoursesResponse,
  CategoriesResponse,
  EnrollmentResponse,
  UnenrollResponse,
  PaginationParams,
} from "~/types";

export const useCoursesService = () => {
  const api = useApi();

  const getCourses = (params: CourseFilters) => {
    return api.get<CoursesResponse>("/courses/", params);
  };

  const getCourse = (slug: string) => {
    return api.get<CourseDetail>(`/courses/${slug}/`);
  };

  const getCategory = (slug: string) => {
    return api.get<Category>(`/categories/${slug}/`);
  };

  const getMyCourses = () => {
    return api.get<CoursesResponse>("/courses/my_courses/?page_size=9999");
  };

  const getCategories = (options: { ordering?: string } & PaginationParams) => {
    return api.get<CategoriesResponse>("/categories/", options);
  };

  const getCourseLessons = (slug: string) => {
    return api.get<any>(`/lessons/`, { course: slug });
  };

  const enrollToCourse = (slug: string) => {
    return api.post<EnrollmentResponse>(`/courses/${slug}/enroll/`);
  };

  const unenrollFromCourse = (slug: string) => {
    return api.post<UnenrollResponse>(`/courses/${slug}/unenroll/`);
  };

  return {
    getCourses,
    getCourse,
    getCategory,
    getMyCourses,
    getCategories,
    getCourseLessons,
    enrollToCourse,
    unenrollFromCourse,
  };
};
