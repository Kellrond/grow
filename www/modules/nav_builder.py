from flask import url_for

class NavBuilder():
    ''' Template for the navbar items. 

        Notes:

    '''
    def html(self) -> str:
        ''' Returns the html for the navbar. Uses a handful of private functions to accomplish this.  '''
        # login     = self.__build_login_form()
        nav_items = self.__build_nav_items()

        html = f'''
            <header class="header">
                <nav class="navbar navbar-expand-md navbar-dark bg-dark fixed-top" style="z-index: 1900; opacity: 95%;">
                    <a class="navbar-brand ms-2" href="{ url_for('home.home') }" style="color: rgb(255, 187, 0);">Garden </a>
                    <button class="navbar-toggler mx-2" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent">
                    <span class="navbar-toggler-icon"></span>
                    </button>
                    <div class="collapse navbar-collapse" id="navbarSupportedContent">
                        { nav_items }
                    </div>
                </nav>  
            </header>
                '''
        return html

    def __build_nav_items(self) -> None:
        ''' Constructs the nav bar items '''
        return f'''
            <ul class="navbar-nav mb-0 ms-2 ">    
                <li class="nav-item">
                    <a class="nav-link" href="{ url_for('documentation.documentation') }">Documentation</a>
                </li>  
            </ul>
            '''