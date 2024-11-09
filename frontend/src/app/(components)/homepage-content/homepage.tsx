import "./homepage.css"

const HomepageContent = () => {
  return (
    <div className="page-container">
      <div className="section">
        <h1 className="info-header">
          Network laboratory supporter
        </h1>
        <p>
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Voluptatum officia nulla eveniet. Praesentium officia dicta vel voluptatem id eos quis porro facilis perferendis quo saepe, inventore a incidunt delectus numquam consequatur ea beatae, cupiditate doloribus nulla! Officiis fugiat quasi eaque ex asperiores debitis perferendis ipsum recusandae in! Autem, rerum laborum.
        </p>
      </div>
      <div className="section">
        <h2 className="sub-header">
          Tool overview
        </h2>
        <p>
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Quam labore id eaque blanditiis ducimus sit voluptates, eum libero rerum non, nulla exercitationem illo corporis commodi ut beatae nostrum! Est fuga dolore, quibusdam itaque sed blanditiis temporibus, ipsa nulla iure aspernatur voluptas reiciendis repudiandae quam saepe aut. Esse placeat atque dicta.
        </p>
      </div>
      <div className="section">
        <h2 className="sub-header">
          Available functionality
        </h2>
        <ul className="func-list">
          <li>Uploading virtual topology configuration to physical devices in network lab</li>
          <li>Downloading physical topology configuration to a portable file</li>
          <li>Management of the set of all physical devices available in laboratory class</li>
        </ul>
      </div>
    </div>
  );
}

export default HomepageContent;