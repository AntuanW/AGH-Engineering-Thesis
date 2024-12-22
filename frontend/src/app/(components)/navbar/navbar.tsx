"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";

import "./navbar.css";

const Navbar = () => {
  const pathname = usePathname();
  const isActive = (href: string) => pathname === href ? "single-link active" : "single-link";

  return (
    <div className="nav-container">
      <ul className="links-container">
        <li className="single-link-container">
          <Link href="/" className={isActive("/")}>
            Upload config
          </Link>
        </li>
        <li className="single-link-container">
          <Link href="/download-config" className={isActive("/download-config")}>
            Download config
          </Link>
        </li>
        <li className="single-link-container">
          <Link href="/manage-devices" className={isActive("/manage-devices")}>
            Manage devices in lab
          </Link>
        </li>
      </ul>
    </div>
  );
}


export default Navbar;