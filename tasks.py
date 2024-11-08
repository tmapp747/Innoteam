from textwrap import dedent

class TaskPrompts():
    def expand():
        return dedent("""
            Analyze and expand this idea by conducting comprehensive research.
    
            Final answer MUST be a comprehensive idea report detailing:
            - Value proposition
            - Target audience
            - Unique selling points
            - Key features and benefits
            - Brand voice and tone
            - Visual design direction
            - Color scheme preferences
            - User experience goals
    
            IDEA: 
            ----------
            {idea}
        """)

    def refine_idea():
        return dedent("""
            Expand idea report with a Why, How, and What messaging 
            strategy using the Golden Circle Communication technique.
            
            Your final answer MUST include:
            - Complete idea report
            - WHY: Core purpose and beliefs
            - HOW: Unique approach and methods
            - WHAT: Products/services offered
            - Core message
            - Key features
            - Supporting arguments
            - Visual design recommendations
            - User interface guidelines
            
            Focus on modern web design principles and user experience.
        """)

    def setup_project():
        return dedent("""
            Set up a modern web development project with the following stack:
            
            1. Next.js 14 with App Router
            2. Shadcn UI for components
            3. Tailwind CSS for styling
            4. TypeScript for type safety
            
            Project Structure:
            /website
                /app
                    /components
                    /lib
                    /styles
                    /types
                    layout.tsx
                    page.tsx
                /public
                    /images
                package.json
                tailwind.config.js
                tsconfig.json
                
            Initialize with:
            1. Git repository
            2. Proper TypeScript configuration
            3. Tailwind CSS setup
            4. Shadcn UI components
            5. ESLint and Prettier
            6. Responsive design utilities
            
            Ensure all modern development practices are followed.
        """)

    def create_components():
        return dedent("""
            Create modern, responsive website components based on the expanded idea.
            
            Requirements:
            1. Use Shadcn UI components
            2. Implement responsive design with Tailwind CSS
            3. Create reusable components
            4. Add modern animations and transitions
            5. Ensure accessibility (WCAG compliance)
            6. Implement dark mode
            7. Optimize performance
            
            Components to create:
            - Navigation (responsive with mobile menu)
            - Hero section (with animations)
            - Features grid
            - About section
            - Testimonials
            - Contact form
            - Footer
            
            Use modern React patterns and best practices.
        """)

    def create_content():
        return dedent("""
            Create compelling website content based on the expanded idea.
            
            Content Requirements:
            1. SEO-optimized headlines
            2. Engaging call-to-actions
            3. Clear value propositions
            4. Feature descriptions
            5. About section content
            6. Contact form copy
            7. Meta descriptions
            
            Follow modern web content principles:
            - Clear hierarchy
            - Scannable text
            - Active voice
            - Emotional triggers
            - Social proof
            - Trust signals
            
            Ensure content aligns with modern design aesthetics.
        """)

    def implement_features():
        return dedent("""
            Implement modern website features and functionality.
            
            Features to implement:
            1. Smooth scroll navigation
            2. Responsive images and layouts
            3. Dark mode toggle
            4. Loading animations
            5. Form validation
            6. Interactive components
            7. Performance optimization
            
            Technical Requirements:
            - Use React hooks effectively
            - Implement proper state management
            - Ensure type safety with TypeScript
            - Follow accessibility guidelines
            - Optimize for Core Web Vitals
            - Implement error boundaries
            - Add proper loading states
        """)

    def qa_review():
        return dedent("""
            Review the website for quality assurance.
            
            Check for:
            1. Responsive design across devices
            2. Performance metrics
            3. Accessibility compliance
            4. Cross-browser compatibility
            5. Loading states
            6. Error handling
            7. Content accuracy
            8. Visual consistency
            9. Interactive features
            10. SEO optimization
            
            Provide detailed feedback for improvements.
        """)

    def optimize():
        return dedent("""
            Optimize the website for performance and user experience.
            
            Optimization areas:
            1. Image optimization
            2. Code splitting
            3. Lazy loading
            4. CSS optimization
            5. JavaScript bundle size
            6. Server-side rendering
            7. Caching strategies
            8. API response times
            
            Focus on Core Web Vitals:
            - Largest Contentful Paint
            - First Input Delay
            - Cumulative Layout Shift
            
            Provide metrics and improvement suggestions.
        """)

    def analyze_improvements():
        return dedent("""
            Analyze the project for potential improvements.
            
            Steps to follow:
            1. Review code quality
            2. Identify performance bottlenecks
            3. Check for security vulnerabilities
            4. Evaluate user experience
            5. Update dependencies
            
            Provide a detailed report with suggestions for enhancements.
        """)
