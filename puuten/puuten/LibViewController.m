//
//  LibViewController.m
//  puuten
//
//  Created by wang jialei on 12-8-17.
//
//

#import "LibViewController.h"
#import "ImageViewCell.h"
#import "WBViewController.h"
#import "BSHeader.h"

@interface LibViewController ()

@end

@implementation LibViewController
@synthesize categ = _categ;

- (void)setCateg:(NSString *)categ{
    _categ = categ;
    NSLog(@"111111");
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
    self.view = [[UIView alloc] initWithFrame:[[UIScreen mainScreen] bounds]];
    
    //[[UINavigationBar appearance] setTintColor:[UIColor blackColor]];
    
    // Build an array of controllers
    NSMutableArray *controllers = [NSMutableArray array];
    
    ContentViewController *info = [[ContentViewController alloc] initWithNibName:@"ContentViewController" bundle:nil];
    info.categ = _categ;
    info.type = @"4";
    info.title = @"资讯";
    [controllers addObject:info];
    
    ContentViewController *display = [[ContentViewController alloc] initWithNibName:@"ContentViewController" bundle:nil];
    display.categ = _categ;
    display.type = @"5";
    display.title = @"逛街";
    [controllers addObject:display];
    
    ContentViewController *feedback = [[ContentViewController alloc] initWithNibName:@"ContentViewController" bundle:nil];
    feedback.categ = _categ;
    feedback.type = @"6";
    feedback.title = @"点评";
    [controllers addObject:feedback];
    tabBarController = [[UITabBarController alloc] init];
    tabBarController.viewControllers = controllers;
    tabBarController.customizableViewControllers = controllers;
    tabBarController.delegate = self;
    
    [self.view addSubview: tabBarController.view];
	// Do any additional setup after loading the view.
}

- (void)viewDidUnload
{
    [super viewDidUnload];
    // Release any retained subviews of the main view.
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    return (interfaceOrientation == UIInterfaceOrientationPortrait);
}




@end
