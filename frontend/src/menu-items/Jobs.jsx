// In src/menu-items/jobs.jsx (or similar)
import { UploadOutlined } from '@ant-design/icons'; // Or a suitable icon

const icons = {
  UploadOutlined,
};

const jobs = {
  id: 'jobs',
  title: 'Jobs',
  type: 'group',
  children: [
    {
      id: 'jobs-list',
      title: 'Jobs List',
      type: 'item',
      url: '/jobs',
      icon: icons.UploadOutlined,
    },
  ],
};

export default jobs;
