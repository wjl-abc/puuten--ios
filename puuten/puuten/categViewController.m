//
//  categViewController.m
//  puuten
//
//  Created by wang jialei on 12-9-23.
//
//

#import "categViewController.h"
#import "JMWhentapped.h"
#import "LibViewController.h"
#import "ContentViewController.h"

@implementation categViewController
//@synthesize button1;
//@synthesize button2;
@synthesize selected_tag;
//@synthesize login_or_not;


- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender
{
    if ([segue.identifier isEqualToString:@"wb_categ"]) {
        LibViewController *lib = (LibViewController *)segue.destinationViewController;
        //ContentViewController *lib = (ContentViewController *)segue.destinationViewController;
        lib.categ = selected_tag;
        //lib.type = @"6";
    }
}


- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        // Custom initialization
    }
    return self;
}

- (void)viewDidLoad
{
    [super viewDidLoad];
	self.classArray = [[NSArray alloc]
                       initWithObjects:@"美食",
                       @"饮品",
                       @"酒吧",
                       @"ktv",
                       @"电影",
                       @"文化艺术",
                       @"购物",
                       @"健身体育",
                       @"酒店",
                       @"教育",
                       nil];
    
    UIImage *img = [UIImage imageNamed:@"11.jpeg"];
    CGRect frame = CGRectMake(0, 0, img.size.width*460/img.size.height, 460);
    UIImageView *imgView = [[UIImageView alloc] initWithFrame:frame];
    [imgView setImage:img];
    [self.view addSubview:imgView];
    
    for(int i=0; i<[self.classArray count]; i++){
        CGRect frame = CGRectMake(20+150*(i%2), 20+95*floor(i/2.0), 130, 75);
        UIButton *button = [[UIButton alloc] initWithFrame:frame];
        [button setTitle:[self.classArray objectAtIndex:i] forState:UIControlStateNormal];
        button.backgroundColor = [UIColor colorWithRed:0.2 green:0.4 blue:0.4 alpha:0.85];
        button.tag = i;
        [button addTarget:self action:@selector(buttonPressed:)
          forControlEvents:UIControlEventTouchUpInside];
        [self.view addSubview:button];
    }
    
}

-(IBAction)buttonPressed:(id)sender{
    int i = [sender tag];
    selected_tag = [self.classArray objectAtIndex:i];
    [self performSegueWithIdentifier:@"wb_categ" sender:self];
}

- (void)viewDidAppear:(BOOL)animated
{
    /*
     if (!login_or_not) {
        [self performSegueWithIdentifier:@"login_beta" sender:self];
    }
     */
    [super viewDidAppear:animated];
}

- (void)viewDidUnload
{
    [super viewDidUnload];
    selected_tag = nil;
    [self setClassArray:nil];
    // Release any retained subviews of the main view.
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    return (interfaceOrientation == UIInterfaceOrientationPortrait);
}

@end
