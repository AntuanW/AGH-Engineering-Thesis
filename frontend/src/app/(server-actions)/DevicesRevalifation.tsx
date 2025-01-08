"use server"
import { revalidateTag } from "next/cache"

export const revalidateDevices = async () => {
    revalidateTag("all-devices");
}