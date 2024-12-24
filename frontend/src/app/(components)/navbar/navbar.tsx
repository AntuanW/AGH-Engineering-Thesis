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
          <Link href="/upload-topology" className={isActive("/upload-topology")}>
            Upload topology
          </Link>
        </li>
        <li className="single-link-container">
          <Link href="/download-topology" className={isActive("/download-topology")}>
            Download topology
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