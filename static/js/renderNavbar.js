
const renderizaNavBar = (idDivNavbar) => {
  const currentPath = window.location.pathname; // Obtem o caminho da URL atual
  let navbar = document.getElementById(idDivNavbar);

  navbar.innerHTML = `
              <div class="container-fluid">
                  <ul class="navbar-nav topbar-nav align-items-center" id="navbarCtes">
                      <li class="nav-item">
                      <a class="nav-link" href="/">
                          <i class="fas fa-comments"></i> Comunicação Interna
                      </a>
                      </li>

                      <li class="nav-item">
                      <a class="nav-link" href="/iscas">
                          <i class="fas fa-chart-line"></i> Relatório de Iscas
                      </a>
                      </li>
                      <li class="nav-item">
                          <a class="nav-link" href="/envio_coletas">
                              <i class="fas fa-truck"></i> Download de Coletas
                          </a>
                      </li>
                      <li class="nav-item">
                          <a class="nav-link" href="/ctes">
                              <i class="fas fa-truck"></i> CT-e
                          </a>
                      </li>

                      <li class="nav-item">
                          <a class="nav-link" href="/cidades_atendidas">
                              <i class="fas fa-city"></i> Cidades Atendidas
                          </a>
                      </li>
                  </ul>
      </div>
  `;}



