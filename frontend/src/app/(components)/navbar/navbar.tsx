import Link from "next/link";
import "./navbar.css";

const Navbar = () => {
  return (
    <div className="nav-container">
      <ul className="links-container">
        <li className="single-link-container">
          <Link href="/" className="single-link">Home</Link>
        </li>
        <li className="single-link-container">
          <Link href="/upload-config" className="single-link">Upload config</Link>
        </li>
        <li className="single-link-container">
          <Link href="/download-config" className="single-link">Download config</Link>
        </li>
        <li className="single-link-container">
          <Link href="/manage-devices" className="single-link">Manage devices in lab</Link>
        </li>
      </ul>
    </div>
  );
}

export default Navbar;