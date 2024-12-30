"use server"
import { revalidateTag } from "next/cache";

export const revalidateIndexDto = async () => {
  revalidateTag("index-dto");
}