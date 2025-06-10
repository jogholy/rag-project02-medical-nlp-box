import React from 'react';
import { Link } from 'react-router-dom';
import { 
  FileCheck, 
} from 'lucide-react';

const Sidebar = ({ width }) => {
  return (
    <div className="bg-white shadow-lg" style={{ width: `${width}px` }}>
      <nav className="mt-5">
        <Link to="/stand" className="flex items-center p-3 text-gray-700 hover:bg-gray-100">
          <FileCheck className="mr-3" /> 金融术语标准化
        </Link>
      </nav>
    </div>
  );
};

export default Sidebar;